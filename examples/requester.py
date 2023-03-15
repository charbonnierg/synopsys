import typing as t
from dataclasses import dataclass, field
from synopsys import create_event, create_flow, create_bus, Message, Play, Service
from synopsys.adapters import NATSPubSub


T = t.TypeVar("T")


@dataclass
class Result(t.Generic[T]):
    data: t.Optional[T] = field(init=False)
    error: t.Optional[str] = field(init=False)
    success: bool = field(init=False)

    def __post_init__(self) -> None:
        raise NotImplementedError("Use Success or Error class instead of Result class.")


@dataclass
class Success(Result[T]):
    data: T = field(init=True)
    error: None = field(init=False, default=None)
    success: bool = field(init=False, default=True)

    def __post_init__(self) -> None:
        """Do not call parent __post_init__ method"""
        pass

    def __bool__(self) -> t.Literal[True]:
        return True


@dataclass
class Error(Result[t.Any]):
    data: None = field(init=False, default=None)
    error: str = field(init=True)
    success: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        """Do not call parent __post_init__ method"""
        pass

    def __bool__(self) -> t.Literal[False]:
        return False


# Create an event
event = create_event(
    "service-command", subject="test.service", schema=int, reply_schema=Result[float]
)

# Create an event bus
bus = create_bus(NATSPubSub())


# Define a requester
async def requester(msg: Message[None, int, None, Result[float]]) -> Result[float]:
    """A function which can fail.

    There is no magic involved. The event is defined as returning a Result,
    so this function MUST return a result.
    There is no middleware or hidden transformation involved.
    If an exceptio is raised, instrumentation may log an error, but nothing else
    will happen !
    """
    try:
        return Success(1 / msg.data)
    except Exception as err:
        return Error(str(err))


play = Play(
    bus, [Service("test-service", create_flow(event), requester)], auto_connect=True
)


if __name__ == "__main__":
    play.main()
