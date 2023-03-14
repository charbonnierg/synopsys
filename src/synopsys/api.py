import typing as t

from .aio.bus import EventBus
from .defaults import DEFAULT_CODEC
from .entities.events import Event
from .entities.flows import Flow, Subscription
from .entities.syntax import SubjectSyntax
from .interfaces.codec import CodecBackend
from .interfaces.pubsub import PubSubBackend
from .operations.subjects import render_subject
from .types import NULL, DataT, MetadataT, ReplyT, ScopeT

__all__ = ["create_event"]


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, None, None]:
    """Create a minimal event without scope, metadata or reply event"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, None, None]:
    """Create an event with a schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, None, None]:
    """Create an event with a scope schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, None, ReplyT]:
    """Create an event with a reply schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: t.Type[MetadataT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, MetadataT, None]:
    """Create an event with a metadata schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, None, None]:
    """Create an event with a schema and a scope schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, None, ReplyT]:
    """Create an event with a schema and a reply schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: None = None,
    metadata_schema: t.Type[MetadataT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, MetadataT, None]:
    """Create an event with a schema and a metadata schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    metadata_schema: None = None,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, None, ReplyT]:
    """Create an event with a reply schema and a scope schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    metadata_schema: t.Type[MetadataT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, None, MetadataT, ReplyT]:
    """Create an event with a reply schema and a metadata schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    metadata_schema: t.Type[MetadataT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, MetadataT, None]:
    """Create an event with a metadata schema and a scope schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: None = None,
    metadata_schema: t.Type[MetadataT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, MetadataT, None]:
    """Create an event with a schema, a metadata schema and a scope schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: None = None,
    reply_schema: t.Type[ReplyT],
    metadata_schema: t.Type[MetadataT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[None, DataT, MetadataT, ReplyT]:
    """Create an event with a schema, a metadata schema and a reply schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: None = None,
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    metadata_schema: t.Type[MetadataT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, None, MetadataT, ReplyT]:
    """Create an event with a reply schema, a metadata schema and a scope schema"""
    ...  # pragma: no cover


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
) -> Event[ScopeT, DataT, None, ReplyT]:
    """Create an event with a schema, a reply schema, and a scope schema"""
    ...  # pragma: no cover


@t.overload
def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Type[DataT],
    scope_schema: t.Type[ScopeT],
    reply_schema: t.Type[ReplyT],
    metadata_schema: t.Type[MetadataT],
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[ScopeT, DataT, MetadataT, ReplyT]:
    """Create an event with a schema, a reply schema, and a scope schema"""
    ...  # pragma: no cover


def create_event(
    name: str,
    subject: str,
    *,
    schema: t.Any = NULL,
    scope_schema: t.Any = NULL,
    reply_schema: t.Any = NULL,
    metadata_schema: t.Any = NULL,
    title: t.Optional[str] = None,
    description: t.Optional[str] = None,
    syntax: t.Optional[SubjectSyntax] = None,
) -> Event[t.Any, DataT, t.Any, t.Any]:
    if schema is None:
        schema = type(None)
    if reply_schema is None:
        reply_schema = type(None)
    if metadata_schema is None:
        metadata_schema = type(None)
    if scope_schema is None:
        scope_schema = type(None)
    # Handle events
    return Event(
        name=name,
        subject=subject,
        schema=schema,
        scope_schema=scope_schema,
        reply_schema=reply_schema,
        metadata_schema=metadata_schema,
        title=title,
        description=description,
        syntax=syntax,
    )


@t.overload
def create_flow(
    source: Event[ScopeT, DataT, MetadataT, ReplyT],
    *,
    emits: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any]]] = None,
    requests: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any]]] = None,
    scope: t.Optional[t.Dict[str, str]] = None,
) -> Subscription[ScopeT, DataT, MetadataT, ReplyT]:
    ...  # pragma: no cover


@t.overload
def create_flow(
    source: None = None,
    *,
    emits: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any]]] = None,
    requests: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any]]] = None,
    scope: t.Optional[t.Dict[str, str]] = None,
) -> Subscription[ScopeT, DataT, MetadataT, ReplyT]:
    ...  # pragma: no cover


def create_flow(
    source: t.Optional[Event[t.Any, t.Any, t.Any, t.Any]] = None,
    *,
    emits: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any]]] = None,
    requests: t.Optional[t.List[Event[t.Any, t.Any, t.Any, t.Any]]] = None,
    scope: t.Optional[t.Dict[str, str]] = None,
) -> Flow:
    """Create a new flow for an event."""
    emits = emits or []
    requests = requests or []
    if scope:
        if not source:
            raise ValueError("filter can only be used when a source is provided")
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
            title=source.title,
            description=source.description,
            syntax=source.syntax,
        )
        return Subscription(
            emits=emits, requests=requests, source=source, filter=source_filter
        )
    elif source:
        return Subscription(
            emits=emits, requests=requests, source=source, filter=source
        )
    return Flow(emits=emits, requests=requests)


def create_bus(
    pubsub: PubSubBackend,
    flow: t.Optional[Flow] = None,
    *,
    codec: CodecBackend = DEFAULT_CODEC,
) -> EventBus:
    return EventBus(flow=flow, pubsub=pubsub, codec=codec)


def __test_annotations() -> None:  # pragma: no cover
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

    # No schema
    evt = create_event("test", "test")
    assert_type(evt, Event[None, None, None, None])

    # Only payload schema
    evt2 = create_event("test", "test", schema=None)
    assert_type(evt2, Event[None, None, None, None])

    # Only payload schema
    evt3 = create_event("test", "test", schema=int)
    assert_type(evt3, Event[None, int, None, None])

    # Only scope schema
    evt4 = create_event("test", "test", scope_schema=None)
    assert_type(evt4, Event[None, None, None, None])

    # Only scope schema
    evt5 = create_event("test", "test", scope_schema=t.Dict[str, str])
    assert_type(evt5, Event[t.Dict[str, str], None, None, None])

    # Only reply schema
    evt6 = create_event("test", "test", reply_schema=None)
    assert_type(evt6, Event[None, None, None, None])

    # Only reply schema
    evt7 = create_event("test", "test", reply_schema=int)
    assert_type(evt7, Event[None, None, None, int])

    # Only metadata schema
    evt8 = create_event("test", "test", metadata_schema=None)
    assert_type(evt8, Event[None, None, None, None])

    # Only metadata schema
    evt9 = create_event("test", "test", metadata_schema=t.Dict[str, str])
    assert_type(evt9, Event[None, None, t.Dict[str, str], None])

    # Schema + Scope schema
    evt10 = create_event("test", "test", schema=int, scope_schema=t.Dict[str, str])
    assert_type(evt10, Event[t.Dict[str, str], int, None, None])

    # Schema + Reply schema
    evt11 = create_event("test", "test", schema=int, reply_schema=int)
    assert_type(evt11, Event[None, int, None, int])

    # Schema + Metadata schema
    evt12 = create_event("test", "test", schema=int, metadata_schema=t.Dict[str, str])
    assert_type(evt12, Event[None, int, t.Dict[str, str], None])

    # Scope schema + Metadata schema
    evt13 = create_event(
        "test", "test", scope_schema=t.Dict[str, str], metadata_schema=t.Dict[str, str]
    )
    assert_type(evt13, Event[t.Dict[str, str], None, t.Dict[str, str], None])

    # Scope Schema + Reply schema
    evt14 = create_event(
        "test", "test", reply_schema=int, scope_schema=t.Dict[str, str]
    )
    assert_type(evt14, Event[t.Dict[str, str], None, None, int])

    # Metadata Schema + Reply schema
    evt15 = create_event(
        "test", "test", reply_schema=int, metadata_schema=t.Dict[str, str]
    )
    assert_type(evt15, Event[None, None, t.Dict[str, str], int])

    # Schema + Scope schema + Metadata schema
    evt16 = create_event(
        "test",
        "test",
        schema=int,
        scope_schema=t.Dict[str, str],
        metadata_schema=t.Dict[str, str],
    )
    assert_type(evt16, Event[t.Dict[str, str], int, t.Dict[str, str], None])

    # Reply schema + Scope schema + Metadata schema
    evt17 = create_event(
        "test",
        "test",
        reply_schema=int,
        scope_schema=t.Dict[str, str],
        metadata_schema=t.Dict[str, str],
    )
    assert_type(evt17, Event[t.Dict[str, str], None, t.Dict[str, str], int])

    # Schema + Reply schema + Scope schema
    evt18 = create_event(
        "test",
        "test",
        schema=int,
        reply_schema=int,
        scope_schema=t.Dict[str, str],
    )
    assert_type(evt18, Event[t.Dict[str, str], int, None, int])

    # Schema + Reply schema + Metadata schema
    evt19 = create_event(
        "test",
        "test",
        schema=int,
        reply_schema=int,
        metadata_schema=t.Dict[str, str],
    )
    assert_type(evt19, Event[None, int, t.Dict[str, str], int])

    # Schema + Reply schema + Scope schema + Metadata schema
    evt20 = create_event(
        "test",
        "test",
        schema=int,
        reply_schema=int,
        scope_schema=t.Dict[str, str],
        metadata_schema=t.Dict[str, str],
    )
    assert_type(evt20, Event[t.Dict[str, str], int, t.Dict[str, str], int])
