"""An example illustrating  to implement a request/reply service
which returns bytes data, but still allow to detect success or failure
using metadata.

Usecases:
    => All the services which do not return JSON data, but return bytes data.

Examples:
    => Load an ONNX model. Models are distributed as bytes. We don't want to transform
    them into hex strings or base64 encoded strings, because then, client would also
    need to decode according to proper encoding. It makes usage through NATS CLI
    more plainful for example (need to pipe and know which UNIX command can be used
    to decode)
"""
import base64
import typing as t
from dataclasses import dataclass

from synopsys import (
    Message,
    Play,
    Reply,
    Service,
    create_bus,
    create_event,
    create_flow,
)
from synopsys.adapters import NATSPubSub

T = t.TypeVar("T")


@dataclass
class ResultMeta:
    """Metadata found in service reply."""

    error: t.Optional[str]
    success: bool


@dataclass
class Success(ResultMeta):
    """Metadata found in successful service reply."""

    error: None = None
    success: t.Literal[True] = True


@dataclass
class Error(ResultMeta):
    """Metadata found in failed service reply."""

    error: str
    success: t.Literal[False] = False


# Create an event
event = create_event(
    "service-command",
    subject="test.service",
    schema=str,
    reply_schema=bytes,
    reply_metadata_schema=ResultMeta,
)

# Create an event bus
bus = create_bus(NATSPubSub())


# Define a usecase
def encode_operation(text: str) -> bytes:
    """Operation does not have the concept of "message".

    It receives some data, and return some other data.
    Additionally, it may raise exceptions.
    """
    if not text:
        raise ValueError("Text is empty")
    return base64.b64encode(text.encode())


# Define a requester handler
async def handler(
    msg: Message[None, str, None, bytes, ResultMeta]
) -> Reply[bytes, ResultMeta]:
    """A service handler must NEVER raise exception.

    It should contain as few logic as possible, calling operations whenever
    it is possible.

    The main responsability of the handler, is to forward data found within
    messages to operations or usecases, and then return a reply.

    There is no magic involved. The event is defined as returning bytes reply,
    so this function must return a bytes reply, regardless of success or failure.

    Moreover, event is defined as returning a reply with metadata, so this function
    must return a reply with appropriate metadata.

    There is no middleware or hidden transformation involved.

    If an exception is raised, instrumentation may log an error, but nothing else
    will happen ! And no reply will be sent !
    """
    try:
        # Return a successful reply
        return Reply(encode_operation(msg.data), Success())
    except Exception as err:
        # Return an error reply
        return Reply(b"", Error(str(err)))


FLOW = create_flow("service-flow", command=event)

play = Play(
    bus,
    actors=[
        Service(FLOW, handler),
    ],
    auto_connect=True,
)


if __name__ == "__main__":
    play.main()
