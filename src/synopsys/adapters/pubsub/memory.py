import typing as t
from asyncio import Queue as AIOQueue
from asyncio import QueueFull, Task, create_task, wait_for
from contextlib import asynccontextmanager
from dataclasses import dataclass
from secrets import token_hex

from synopsys.entities.syntax import SubjectSyntax
from synopsys.interfaces.pubsub import PubSubBackend, PubSubMsg
from synopsys.operations.subjects import match_subject


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
        self.subscribers: t.List[t.Tuple[str, str, AIOQueue[InMemoryMsg]]] = []
        self.responders: t.List[
            t.Tuple[
                str,
                str,
                AIOQueue[InMemoryMsg],
            ],
        ] = []

    async def __request_event(self, request: InMemoryMsg) -> InMemoryMsg:
        """Wait for a single event."""
        if not request.reply_subject:
            raise ValueError("Cannot request event without reply subject")
        async with self.subscribe(request.reply_subject) as observer:
            self.__notify_request(request)
            async for event in observer:
                return event
        raise ValueError("No reply received")

    async def publish(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> None:
        msg = InMemoryMsg(subject, payload, headers)
        self.__notify_msg(msg)

    async def request(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> InMemoryMsg:
        """Request an event."""
        reply_subject: str = token_hex(16)
        req = InMemoryMsg(subject, payload, headers, reply_subject)
        msg = await wait_for(self.__request_event(req), timeout=timeout)
        return msg

    def __notify_msg(self, msg: InMemoryMsg) -> None:
        """Distribue message to subscribers."""
        queues_processed: t.Set[str] = set()
        for target, queue, observer in self.subscribers:
            if queue and queue in queues_processed:
                continue
            if not match_subject(target, msg.subject, self.syntax):
                continue
            try:
                observer.put_nowait(msg)
            except QueueFull:
                continue
            else:
                if queue:
                    queues_processed.add(queue)

    def __notify_request(self, request: InMemoryMsg) -> None:
        """Distribute request to subscribers."""
        queues_processed: t.Set[str] = set()
        for target, queue, responder in self.responders:
            if queue and queue in queues_processed:
                continue
            if not match_subject(target, request.subject, self.syntax):
                continue
            try:
                responder.put_nowait(request)
            except QueueFull:
                continue
            else:
                if queue:
                    queues_processed.add(queue)

    @asynccontextmanager
    async def subscribe(
        self,
        subject: str,
        queue: t.Optional[str] = None,
    ) -> t.AsyncIterator[t.AsyncIterator[InMemoryMsg]]:
        """Create a new observer, optionally within a queue."""
        queue = queue or ""
        observer: "AIOQueue[InMemoryMsg]" = AIOQueue()
        key = (subject, queue, observer)
        self.subscribers.append(key)
        current_task: t.Optional["Task[InMemoryMsg]"] = None

        async def iterator() -> t.AsyncIterator["InMemoryMsg"]:
            nonlocal current_task
            nonlocal observer
            while True:
                current_task = create_task(observer.get())
                yield await wait_for(current_task, timeout=None)

        try:
            yield iterator()
        finally:
            if current_task:
                current_task.cancel()
            self.subscribers.remove(key)
