import asyncio
import typing as t
from contextlib import asynccontextmanager
from dataclasses import dataclass

from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg

from synopsys.errors import BusDisconnectedError, SubscriptionClosedError
from synopsys.interfaces import PubSubBackend, PubSubMsg


@dataclass
class NATSMsg(PubSubMsg):
    """NATS message interface."""

    def __init__(self, msg: Msg) -> None:
        self.msg = msg

    def get_subject(self) -> str:
        """Get message subject as string."""
        return self.msg.subject

    def get_payload(self) -> bytes:
        """Get message payload as bytes."""
        return self.msg.data

    def get_headers(self) -> t.Dict[str, str]:
        """Get message headers as string mapping."""
        return self.msg.headers or {}

    def get_reply_subject(self) -> t.Optional[str]:
        """Get reply subject from message when it exists."""
        return self.msg.reply or None


class NATSPubSub(PubSubBackend):
    """An implementation of PubSubBackend using NATS.

    This implementation relies on [nats-py[1]](#1) library.

    References:
    1. [`nats-py`](https://github.com/nats-io/nats.py)
    """

    def __init__(self) -> None:
        """Create a new NATS client."""
        self.nc = NATSClient()

    async def publish(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> None:
        """Publish a message on given subject."""
        if self.nc.is_closed or self.nc.is_draining:
            raise BusDisconnectedError()
        await self.nc.publish(subject=subject, payload=payload, headers=headers)
        if timeout:
            await self.nc.flush(timeout=timeout)  # type: ignore[arg-type]

    async def request(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> NATSMsg:
        """Send a request on given subject and wait for a reply."""

        reply = await self.nc.request(
            subject=subject,
            payload=payload,
            headers=headers,
            timeout=timeout,  # type: ignore[arg-type]
        )
        return NATSMsg(reply)

    @asynccontextmanager
    async def subscribe(
        self, subject: str, queue: t.Optional[str] = None
    ) -> t.AsyncIterator[t.AsyncIterator[PubSubMsg]]:
        """Subscribe to messages published on given subject."""

        # Create a subscription
        sub = await self.nc.subscribe(subject=subject, queue=queue or "")
        # Create a future in case context manager is closed
        closed: "asyncio.Future[None]" = asyncio.Future()

        async def _next_msg() -> Msg:
            msg = await sub._pending_queue.get()
            sub._pending_size -= len(msg.data)
            return msg

        # Define an async iterator
        async def iterator() -> t.AsyncIterator[NATSMsg]:
            # Wait for the first of:
            #  * the future indicating that context is closed
            #  * the next message
            while True:
                next_msg = asyncio.create_task(_next_msg())
                done, _ = await asyncio.wait(
                    (next_msg, closed), return_when=asyncio.FIRST_COMPLETED
                )
                if closed in done:
                    next_msg.cancel()
                    await asyncio.wait([next_msg], timeout=None)
                    raise SubscriptionClosedError()
                yield NATSMsg(next_msg.result())

        # Yield asyc iterator
        try:
            yield iterator()
        finally:
            closed.set_result(None)
            # Delete subscrition
            await sub.unsubscribe()

    async def connect(self) -> None:
        """Connect to remote NATS server."""
        await self.nc.connect(connect_timeout=2)

    async def disconnect(self) -> None:
        """Disconnect from remote NATS server."""
        if self.nc.is_closed or self.nc._status == self.nc.DISCONNECTED:
            return
        await self.nc.close()
