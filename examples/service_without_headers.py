"""An example illustrating  to implement a request/reply service
which returns generic JSON data, allowing to detect success or failure
WITHOUT any need for metadata.

Usecases:
    => All the services which return JSON data and might fail.

Examples:
    => 99% of our services.
"""
import typing as t
from dataclasses import dataclass, field
from synopsys import (
    create_event,
    create_flow,
    create_bus,
    Message,
    Play,
    Service,
    SimpleReply,
)
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
async def requester(
    msg: Message[None, int, None, Result[float], None]
) -> SimpleReply[Result[float]]:
    """A service handler must NEVER raise exception.

    It should contain as few logic as possible, calling operations whenever
    it is possible.

    The main responsability of the handler, is to forward data found within
    messages to operations or usecases, then to return a reply.

    There is no magic involved. The event is defined as returning Result[float] reply,
    so this function must return a Result[float] reply, regardless of success or failure.

    Moreover, event is defined WITHOUT metadata, so this function
    must return a reply WITHOUT metadata.

    There is no middleware or hidden transformation involved.

    If an exception is raised, instrumentation may log an error, but nothing else
    will happen ! And no reply will be sent !
    """
    try:
        return SimpleReply(Success(1 / msg.data))
    except Exception as err:
        return SimpleReply(Error(str(err)))


FLOW = create_flow(command=event)


play = Play(bus, [Service("base64-encode", FLOW, requester)], auto_connect=True)


if __name__ == "__main__":
    play.main()
