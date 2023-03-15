import typing as t

from ..entities import Actor, Message

if t.TYPE_CHECKING:
    from ..aio.play import Play  # pragma: no cover


T = t.TypeVar("T")


class PlayInstrumentation:
    """Configure how a play should be instrumented."""

    def actor_starting(self, play: "Play", actor: Actor) -> None:
        """Observe actor starting."""

    def actor_started(self, play: "Play", actor: Actor) -> None:
        """Observe actor started."""

    def actor_cancelled(self, play: "Play", actor: Actor) -> None:
        """Observe actor cancelled."""

    def event_processing_failed(
        self,
        play: "Play",
        actor: Actor,
        msg: Message[t.Any, t.Any, t.Any, t.Any],
        exc: BaseException,
    ) -> None:
        """Observe an exception raised by an actor."""

    def event_received(
        self,
        play: "Play",
        actor: Actor,
        msg: Message[t.Any, t.Any, t.Any, t.Any],
    ) -> None:
        """Observe a received message"""

    def event_processed(
        self,
        play: "Play",
        actor: Actor,
        msg: Message[t.Any, t.Any, t.Any, t.Any],
    ) -> None:
        """Observe a successful event processed"""

    def play_starting(self, play: "Play") -> None:
        """Observe play starting."""

    def play_started(self, play: "Play") -> None:
        """Observe play started."""

    def play_stopping(self, play: "Play") -> None:
        """Observe play stopping."""

    def play_failed(self, play: "Play", errors: t.List[BaseException]) -> None:
        """Observe play failed."""

    def play_stopped(self, play: "Play") -> None:
        """Observe play stopped."""
