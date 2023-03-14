import typing as t
from dataclasses import dataclass, field

from ..entities.actors import Actor
from .bus import EventBus


@dataclass
class Play:
    bus: EventBus
    actors: t.List[Actor] = field(default_factory=list)

    def with_actors(self, *actors: Actor) -> "Play":
        """Add actors to the play."""
        self.actors.extend(actors)
        return self

    def main(self) -> None:
        raise NotImplementedError
