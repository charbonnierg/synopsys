import abc
import typing as t
from types import TracebackType

BackendT = t.TypeVar("BackendT", bound="PubSubBackend")


class PubSubMsg(metaclass=abc.ABCMeta):
    """PubSub message interface."""

    @abc.abstractmethod
    def get_payload(self) -> bytes:
        """Get message payload as bytes."""
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def get_headers(self) -> t.Dict[str, str]:
        """Get message headers as string mapping."""
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def get_subject(self) -> str:
        """Get message subject as string."""
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def get_reply_subject(self) -> t.Optional[str]:
        """Get reply subject as string if it is defined."""
        raise NotImplementedError  # pragma: no cover


class PubSubBackend(metaclass=abc.ABCMeta):
    """Pubsub backend interface."""

    @abc.abstractmethod
    async def publish(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> None:
        """Publish a message on given subject."""
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    async def request(
        self,
        subject: str,
        payload: bytes,
        headers: t.Dict[str, str],
        timeout: t.Optional[float] = None,
    ) -> PubSubMsg:
        """Send a request and wait for a reply."""
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def subscribe(
        self,
        subject: str,
        queue: t.Optional[str] = None,
    ) -> t.AsyncContextManager[t.AsyncIterator[PubSubMsg]]:
        """Subscribe to events published on given subject."""
        raise NotImplementedError  # pragma: no cover

    async def connect(self) -> None:
        """Connect to remote pubsub."""

    async def disconnect(self) -> None:
        """Disconnect from remote pubsub."""

    async def __aenter__(self: BackendT) -> BackendT:
        """Connect on context enter."""
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
