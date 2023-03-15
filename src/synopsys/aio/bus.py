import typing as t
from contextlib import asynccontextmanager
from dataclasses import dataclass
from types import TracebackType

from ..entities.events import Event
from ..entities.flows import Flow, Subscription
from ..entities.messages import Message
from ..interfaces.codec import CodecBackend
from ..interfaces.pubsub import PubSubBackend, PubSubMsg
from ..types import DataT, MetadataT, ReplyT, ScopeT
from .waiter import RequestWaiter, Waiter


@dataclass
class _Request(Message[ScopeT, DataT, MetadataT, ReplyT]):
    reply_subject: str


BusT = t.TypeVar("BusT", bound="EventBus")


class EventBus:
    """An interface used to publish events."""

    def __init__(
        self, pubsub: PubSubBackend, codec: CodecBackend, flow: t.Optional[Flow] = None
    ) -> None:
        self.pubsub = pubsub
        self.codec = codec
        self.flow = flow

    def bind_flow(self, flow: Flow) -> "EventBus":
        """Create a new event bus scoped to a flow."""
        return self.__class__(self.pubsub, self.codec, flow=flow)

    def _create_message(
        self, msg: PubSubMsg, event: Event[ScopeT, DataT, MetadataT, ReplyT]
    ) -> Message[ScopeT, DataT, MetadataT, ReplyT]:
        """Create a typed message out of a pubsub message."""
        subject = msg.get_subject()
        reply_subject = msg.get_reply_subject()
        scope = event.extract_scope(subject, codec=self.codec)
        data = self.codec.decode_payload(msg.get_payload(), event.schema)
        metadata = self.codec.decode_headers(msg.get_headers(), event.metadata_schema)
        if not reply_subject:
            return Message(
                subject=subject,
                scope=scope,
                data=data,
                metadata=metadata,
                event=event,
            )
        return _Request(
            subject=subject,
            scope=scope,
            data=data,
            metadata=metadata,
            event=event,
            reply_subject=reply_subject,
        )

    async def reply(
        self,
        message: Message[ScopeT, DataT, MetadataT, ReplyT],
        data: ReplyT,
        *,
        metadata: MetadataT = ...,  # type: ignore[assignment]
        timeout: t.Optional[float] = None,
    ) -> None:
        """Publish and wait until event is flushed by underlying messaging system."""
        if not isinstance(message, _Request):
            return
        if metadata is ...:
            metadata = {}  # type: ignore[assignment]
        subject = message.reply_subject
        headers = self.codec.encode_headers(metadata)
        payload = self.codec.encode_payload(data)
        return await self.pubsub.publish(
            subject=subject, payload=payload, headers=headers, timeout=timeout
        )

    async def publish(
        self,
        event: Event[ScopeT, DataT, MetadataT, t.Any],
        data: DataT,
        *,
        scope: ScopeT = ...,  # type: ignore[assignment]
        metadata: MetadataT = ...,  # type: ignore[assignment]
        timeout: t.Optional[float] = None,
    ) -> None:
        """Publish and wait until event is flushed by underlying messaging system."""
        if self.flow and event not in self.flow.emits:
            raise ValueError(
                "Cannot publish an event not declared in flow. Append the event to the emits attribute of the flow in order to fix this error."
            )
        if scope is ...:
            scope = {}  # type: ignore[assignment]
        if metadata is ...:
            metadata = {}  # type: ignore[assignment]
        subject = event.get_subject(scope, self.codec)
        headers = self.codec.encode_headers(metadata)
        payload = self.codec.encode_payload(data)
        return await self.pubsub.publish(
            subject=subject, payload=payload, headers=headers, timeout=timeout
        )

    async def request(
        self,
        event: Event[ScopeT, DataT, MetadataT, ReplyT],
        data: DataT,
        *,
        scope: ScopeT = ...,  # type: ignore[assignment]
        metadata: MetadataT = ...,  # type: ignore[assignment]
        timeout: t.Optional[float] = None,
    ) -> ReplyT:
        """Request and wait for reply."""
        if self.flow and event not in self.flow.requests:
            raise ValueError(
                "Cannot request an event not declared in flow. Append the event to the emit attribute of the flow in order to fix this error."
            )
        if scope is ...:
            scope = {}  # type: ignore[assignment]
        if metadata is ...:
            metadata = {}  # type: ignore[assignment]
        subject = event.get_subject(scope, self.codec)
        headers = self.codec.encode_headers(metadata)
        payload = self.codec.encode_payload(data)
        reply = await self.pubsub.request(
            subject=subject, payload=payload, headers=headers, timeout=timeout
        )
        return self.codec.decode_payload(reply.get_payload(), event.reply_schema)

    @asynccontextmanager
    async def subscribe(
        self,
        event: Event[ScopeT, DataT, MetadataT, ReplyT],
        queue: t.Optional[str] = None,
    ) -> t.AsyncIterator[t.AsyncIterator[Message[ScopeT, DataT, MetadataT, ReplyT]]]:
        """Create an event observer.

        An event observer is an asynchronous context manager yielding an
        asynchronous iterator.
        This iterator can be used to iterate over received messages.
        Each message contains both event definition and event data.

        Arguments:
            event: An event to observe
            queue: An optional string indicating that observer belongs to a queue group.
                Within a queue group, each message is delivered to a single observer.

        Returns:
            An asynchronous context manager yielding an asynchronous iterator of messages.
        """
        if self.flow:
            if not isinstance(self.flow, Subscription):
                raise TypeError(
                    "Flow does not have a source declared. Add a source to the flow in order to fix this error."
                )
            elif event != self.flow.source:
                raise TypeError(
                    f"Can only subscribe to the flow source. Tried to subscribe to event {event.name} but flow source is {self.flow.source.name}"
                )

        async with self.pubsub.subscribe(event._subject, queue=queue) as subscription:

            async def iterator() -> t.AsyncIterator[
                Message[ScopeT, DataT, MetadataT, ReplyT]
            ]:
                async for msg in subscription:
                    try:
                        yield self._create_message(msg, event)
                    except Exception:
                        # TODO: It may not be a good idea to simply skip
                        continue

            yield iterator()

    async def next_event(
        self, event: Event[ScopeT, DataT, MetadataT, ReplyT]
    ) -> Message[ScopeT, DataT, MetadataT, ReplyT]:
        async with self.subscribe(event) as subscription:
            async for msg in subscription:
                return msg
        raise ValueError("Did not receive a message")

    async def wait_in_background(
        self, event: Event[ScopeT, DataT, MetadataT, ReplyT]
    ) -> Waiter[Message[ScopeT, DataT, MetadataT, ReplyT]]:
        """Start waiting in background"""
        return await Waiter.create(self.subscribe(event))

    async def request_in_background(
        self,
        event: Event[ScopeT, DataT, MetadataT, ReplyT],
        data: DataT,
        *,
        scope: ScopeT = ...,  # type: ignore[assignment]
        metadata: MetadataT = ...,  # type: ignore[assignment]
        timeout: t.Optional[float] = None,
    ) -> RequestWaiter[ReplyT]:
        """Send a request and wait in background."""
        return await RequestWaiter.create(
            self.request(event, data, scope=scope, metadata=metadata, timeout=timeout)
        )

    async def connect(self) -> None:
        """Connect event bus.

        Calls the .connect() method of the pubsub backend.
        """
        await self.pubsub.connect()

    async def disconnect(self) -> None:
        """Disconnect event bus.

        Calls the .disconnect() method of the pubsub backend.
        """
        await self.pubsub.disconnect()

    async def __aenter__(self: BusT) -> BusT:
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: t.Optional[t.Type[BaseException]] = None,
        exc: t.Optional[BaseException] = None,
        traceback: t.Optional[TracebackType] = None,
    ) -> None:
        """Disconnect on context exit."""
        await self.disconnect()
