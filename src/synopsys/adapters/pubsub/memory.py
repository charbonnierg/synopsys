import logging
import typing as t
from contextlib import asynccontextmanager
from dataclasses import dataclass
from secrets import token_hex

from anyio import ClosedResourceError, create_memory_object_stream

from synopsys.entities.syntax import SubjectSyntax
from synopsys.errors import BusDisconnectedError, SubscriptionClosedError
from synopsys.interfaces.pubsub import PubSubBackend, PubSubMsg
from synopsys.operations.subjects import match_subject

logger = logging.getLogger("pubsub.memory")


@dataclass
class InMemoryMsg(PubSubMsg):
    """An in-memory message."""

    subject: str
    payload: bytes
    headers: t.Dict[str, str]
    reply_subject: t.Optional[str] = None

    def get_payload(self) -> bytes:
        """Get message payload as bytes."""
        return self.payload

    def get_headers(self) -> t.Dict[str, str]:
        """Get message headers as a string mapping."""
        return self.headers

    def get_subject(self) -> str:
        """Get message subject as a string."""
        return self.subject

    def get_reply_subject(self) -> t.Optional[str]:
        """Get reply subject as a string, or None when no reply is expected."""
        return self.reply_subject


class _Observer:
    def __init__(self, subject: str, syntax: SubjectSyntax) -> None:
        self._send, self._receive = create_memory_object_stream(
            max_buffer_size=1, item_type=InMemoryMsg
        )
        self.subject = subject
        self.syntax = syntax

    async def deliver(self, msg: InMemoryMsg) -> None:
        if not match_subject(self.subject, msg.subject, self.syntax):
            return
        await self._send.send(msg)

    async def receive(self) -> InMemoryMsg:
        return await self._receive.receive()


class InMemoryPubSub(PubSubBackend):
    """Implementation of an in-memory pub-sub backend.

    This backend can be used to:
        - publish messages
        - request messages
        - subscribe to messages

    It cannot be used to fetch messages from a queue like
    stream consumers do yet.
    """

    def __init__(self, syntax: t.Optional[SubjectSyntax] = None) -> None:
        """Create a new in-memory pubsub backend.

        By default, NATS syntax is used for subjects.
        """
        self.syntax = syntax or SubjectSyntax()
        self.observers: t.List[_Observer] = []
        self._closed = False

    async def __notify_msg(self, msg: InMemoryMsg) -> None:
        """Distribue message to subscribers."""
        if self._closed:
            raise BusDisconnectedError()
        # Make a copy before iteration because observers is mutated within loop
        for observer in list(self.observers):
            try:
                await observer.deliver(msg)
            except ClosedResourceError:
                # Remote observers which are closed
                self.observers.remove(observer)
                continue

    async def publish(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> None:
        """Publish a message.

        In order to publish an in-memory message, we just need to notify subscribers.
        """
        if self._closed:
            raise BusDisconnectedError()
        msg = InMemoryMsg(subject, payload, headers)
        await self.__notify_msg(msg)

    async def request(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> InMemoryMsg:
        """Request an event.

        In order to request an in-memory message, we need to create a waiter then notify responders
        and finally wait for reply.
        """
        if self._closed:
            raise BusDisconnectedError()
        # Generate a new reply subject
        reply_subject: str = token_hex(16)
        # Generate a new message with the reply subject
        req = InMemoryMsg(subject, payload, headers, reply_subject)
        # Create a new observer on reply subject
        observer = _Observer(reply_subject, self.syntax)
        self.observers.append(observer)
        # Notify the subscribers
        try:
            await self.__notify_msg(req)
            # Return reply
            try:
                return await observer.receive()
            except ClosedResourceError as exc:
                raise SubscriptionClosedError from exc
        finally:
            self.observers.remove(observer)

    @asynccontextmanager
    async def subscribe(
        self,
        subject: str,
        queue: t.Optional[str] = None,
    ) -> t.AsyncIterator[t.AsyncIterator[InMemoryMsg]]:
        """Create a new observer, optionally within a queue."""
        if self._closed:
            raise BusDisconnectedError()
        queue = queue or ""
        observer = _Observer(subject, self.syntax)
        self.observers.append(observer)

        async def iterator() -> t.AsyncIterator[InMemoryMsg]:
            while True:
                try:
                    yield await observer.receive()
                except ClosedResourceError:
                    raise SubscriptionClosedError()

        try:
            yield iterator()
        finally:
            try:
                await observer._receive.aclose()
                await observer._send.aclose()
            except ClosedResourceError:
                pass
            finally:
                self.observers.remove(observer)

    async def disconnect(self) -> None:
        if self._closed:
            return
        self._closed = True
        for observer in self.observers:
            try:
                await observer._send.aclose()
            except ClosedResourceError:
                continue
        for observer in self.observers:
            try:
                await observer._receive.aclose()
            except ClosedResourceError:
                continue
