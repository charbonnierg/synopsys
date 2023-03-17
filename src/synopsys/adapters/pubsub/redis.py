import asyncio
import typing as t
import warnings
from contextlib import asynccontextmanager
from secrets import token_hex

import aioredis
from anyio import fail_after

from synopsys.errors import BusDisconnectedError, SubscriptionClosedError
from synopsys.interfaces import PubSubBackend, PubSubMsg


class RedisMsg(PubSubMsg):
    def __init__(self, msg: t.Dict[str, bytes]) -> None:
        self.msg = msg
        self._subject, *_reply_tokens = (
            self.msg["channel"].decode("utf-8").split(".$REPLY.")
        )
        self._reply_tokens = "".join(_reply_tokens)
        self._reply_subject = (
            "$REPLY." + self._reply_tokens if self._reply_tokens else None
        )

    def get_payload(self) -> bytes:
        return self.msg["data"]

    def get_headers(self) -> t.Dict[str, str]:
        return {}

    def get_subject(self) -> str:
        return self._subject

    def get_reply_subject(self) -> t.Optional[str]:
        return self._reply_subject


class RedisPubSub(PubSubBackend):
    def __init__(self) -> None:
        self.redis = aioredis.Redis.from_url(
            "redis://localhost", max_connections=10, decode_responses=False
        )
        prefix = token_hex(8)
        self._reply_prefix = f"$REPLY.{prefix}"
        self._reply_channel = self.redis.pubsub()
        self._reply_map: t.Dict[str, asyncio.Future[RedisMsg]] = {}
        self._reply_process_task: t.Optional[asyncio.Task[None]] = None
        self._closed = False

    def _process_reply(self, reply: t.Optional[t.Dict[str, bytes]]) -> None:
        if reply is None:
            return
        msg = RedisMsg(reply)
        # Extract reply subject from the redis message
        subject = msg.get_subject()
        if not subject:
            return
        # Check and set reply future
        if self._reply_map and not self._reply_map[subject].done():
            self._reply_map[subject].set_result(msg)
        # Pop reply future
        self._reply_map.pop(subject, None)

    async def connect(self) -> None:
        """A subscription the a reply channel with random prefix is established
        on connection. A task is also started in order to set asyncio Futures
        in reply map each time a message is received on the reply channel."""
        reply_channel = self._reply_prefix + ".*"
        await self._reply_channel.psubscribe(**{reply_channel: self._process_reply})
        self._reply_process_task = asyncio.create_task(self._reply_channel.run())

    async def disconnect(self) -> None:
        """Unsubscribe from reply channel on disconnection."""
        try:
            self._closed = True
            await self._reply_channel.punsubscribe()
            await self._reply_channel.close()
            await self.redis.close()
            await self.redis.connection_pool.disconnect()
        finally:
            if self._reply_process_task:
                if not self._reply_process_task.done():
                    self._reply_process_task.cancel()
                    await asyncio.wait([self._reply_process_task])
                elif not self._reply_process_task.cancelled():
                    self._reply_process_task.exception()

    async def publish(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> None:
        if self._closed:
            raise BusDisconnectedError()
        if headers:
            warnings.warn("Using error is not supported with redis")
        with fail_after(timeout):
            await self.redis.publish(subject, payload)

    async def request(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> RedisMsg:
        if headers:
            warnings.warn("Using headers is not supported with redis")
        reply_token = token_hex(12)
        reply_subject = f"{self._reply_prefix}.{reply_token}"
        subject = f"{subject}.{reply_subject}"
        # Create a new future
        future: asyncio.Future[RedisMsg] = asyncio.Future()
        # Save future in reply map
        self._reply_map[reply_subject] = future
        # Publish then wait for reply
        try:
            with fail_after(timeout):
                # Publish a message
                await self.redis.publish(subject, message=payload)
                return await future
        except TimeoutError:
            if not future.done():
                future.cancel()
            raise

    @asynccontextmanager
    async def subscribe(
        self,
        subject: str,
        queue: t.Optional[str] = None,
        reply: bool = False,
    ) -> t.AsyncIterator[t.AsyncIterator[RedisMsg]]:
        if queue:
            warnings.warn("Using a queue is not supported with redis")
        if reply:
            subject = f"{subject}*"
        pubsub = self.redis.pubsub()
        await pubsub.psubscribe(subject, decode_responses=False)
        # Create a future in case context manager is closed
        closed: "asyncio.Future[None]" = asyncio.Future()

        async def iterator() -> t.AsyncIterator[RedisMsg]:
            while True:
                next_msg = asyncio.create_task(
                    pubsub.get_message(ignore_subscribe_messages=True, timeout=5)
                )
                done, _ = await asyncio.wait(
                    (next_msg, closed), return_when=asyncio.FIRST_COMPLETED
                )
                if closed in done:
                    next_msg.cancel()
                    await asyncio.wait([next_msg], timeout=None)
                    raise SubscriptionClosedError()
                message = next_msg.result()
                # Wait for the future
                if message is None:
                    continue
                yield RedisMsg(message)

        try:
            yield iterator()
        finally:
            if not closed.done():
                closed.set_result(None)
            await pubsub.punsubscribe()
