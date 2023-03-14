import typing as t
from dataclasses import dataclass

from synopsys import (
    EventBus,
    Message,
    Play,
    Subscriber,
    create_bus,
    create_event,
    create_flow,
)
from synopsys.adapters import InMemoryPubSub


@dataclass
class EventScope:
    """Metadata required to construct event subject.

    In this example application, events are delivered for a location and a device ID.
    """

    location: str
    device_id: str


@dataclass
class MeasurementMeta:
    """Metadata found in measuremet event headers.

    In this example application, measurement events have one required metadata field and one optional.
    """

    test: bool
    unit: t.Optional[str]


# Define an event using the above metadata
# Defining event is crucial in order to benefit from typechecking
# The 4 generic typevars of an event are:
#   * the scope schema
#   * the payload schema
#   * the metadata schema
#   * the reply schema (in case event can be requested)
# Bring your cursor onto MEASUREMENT_EVENT to see type annotations
MEASUREMENT_EVENT = create_event(
    "measurement",
    "sensors.{location}.{device_id}.measure",
    schema=int,
    scope_schema=EventScope,
    metadata_schema=MeasurementMeta,
    description="An event holding device measurement as integer",
)


@dataclass
class ProcessingDoneMeta:
    """Metadata found in processing-done event headers"""

    process_duration: float


# Define another event

PROCESSING_DONE = create_event(
    "processing-done",
    "sensors.{location}.{device_id}.processing_done",
    schema=None,
    scope_schema=EventScope,
    metadata_schema=ProcessingDoneMeta,
    description="An event indicating that a measurement has been processed",
)

# This is how we define a logical flow
# Right now, there is no "handler", this is juste about defining
# relations and scope
# Note that flow here is created as a global variable,
# but it can also be generated on the fly on application startup
# (contrary to events, which must be declared BEFORE in order to benefit the most from typechecking)
# A flow is also typed according to its source event
flow = create_flow(
    MEASUREMENT_EVENT,
    emits=[PROCESSING_DONE],
    scope={"location": "westus"},
)

# This is how we define a handler


class Handler:
    """An event handler.

    In order to unit test this handler, it's possible to provide a fake event bus during init.
    When calling the handler, it's possible to craft an InMemoryMsg.
    """

    def __init__(self, bus: EventBus) -> None:
        """Because this handler needs to emit an other event, it must take a bus as argument."""
        self.bus = bus

    async def __call__(
        self, msg: Message[EventScope, int, MeasurementMeta, None]
    ) -> None:
        """Process messages for a specific event."""
        # Emit an event indicating that event was processed
        # Dependending on event bus provided at init, an error
        # may be raised because bus is not allowed to publish to event
        await self.bus.publish(
            # We do not target a suject, instead we target an event !
            PROCESSING_DONE,
            # mypy would tell us if data was not None (because event defines reply schema as None)
            data=None,
            # mypy would tell us if scope was not ok right type
            scope=msg.scope,
            # same thing here, mypy would tell us if metadata were not of right type
            metadata=ProcessingDoneMeta(process_duration=0),
        )


# The code below in the "plumbing" required to "start applications"

# At this point we need some publish/subscribe backend
pubsub = InMemoryPubSub()
# And finally to create a play
# It this line who tells:
#  The callable Handler will be used to process events received by flow source event
#  Moreover, we handler can only publish/request events declared within flow
# But unless we use dependency injection, I don't see how we could automate this...
play = Play(
    bus=create_bus(pubsub),
    # This is not implemented yet (at least not in this version)
    # But the idea is that a "play" can start "actors" in a task group
    # When play is started, all actors are started
    # When play is stopped, all actors are stopped
    # This much is easy to support
    # What could be more complicated is to defined some policies like "on-failure: restart"
    # or "on-failure: shutdown"... It is not planned at the moment because we do not support
    # it using NATS either.
    # Moreover, we would be better off exposing a healthcheck endpoint in our applications
    # and let the orchestrator restart the whole app in case of crash.
    actors=[
        # mypy would detect an error if handler did not have the proper signature
        # according to flow definition
        Subscriber(
            # Subscribe will subscribe to flow source
            flow,
            # Handler event bus is scoped
            Handler(create_bus(pubsub, flow)),
        ),
        # We could also create producers
        # Producer(flow=some_other_flow, task_factory=some_coroutine_function),
    ],
)
# Bonus: From the play alone, we can infer a DAG !
# Since each flow defines its source (if any) and the
# events it notifies/consumes, we can get a pretty good
# view of what's happening within the application !

# The benefits:
#  - The two most valuable benefits are:
#     * type checking everywhere
#     * the fact that we target events and not subjects
#  - Another benefit is the fact that we draw a clear limit
#    between domain and infrastructure.
#    Infrastructure deals with messages, payload, headers and subjects.
#    Domain deals with events, scope, data and metadata.
#  - Another benefit is that we can generate documentation,
#    and it could be some very valuable documentation...
#    We could generate first a DAG using the topological sorter in python standard lib
#    and then we can generate mermaidjs or d2 diagrams
#  - Yet another benefit is that we make it possible to use other message
#    brokers. I think that out of all the attempts I made in the past,
#    this is the best design proposal
#  - Finally, there is 0 magic involved. No decorator, no injection,
#    (altough a lot of type overloading is performed in api module)
#    Most objects are plain python objects
# We can now start the play
if __name__ == "__main__":
    play.main()
