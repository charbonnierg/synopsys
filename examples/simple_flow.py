"""USECASE:

1. Listen for events on "sensors.{location}.{device_id}.measure" and process ingested data
2. Publish a notification when processing is done on "sensors.{location}.{device_id}.processing_done"

Below is a proposal python API to facilitate domain-driven-development and event-driven architecture.

This file is a single-file python module for the sake of simplicity, but in practice, code could
be splitted into several files. The parts which can be split are separated by '######' lines.
"""
import typing as t
from dataclasses import dataclass
import logging

from synopsys import (
    EventBus,
    Message,
    Play,
    Subscriber,
    create_bus,
    create_event,
    create_flow,
)
from synopsys.adapters import NATSPubSub
from synopsys.interfaces.instrumentation import PlayInstrumentation, Actor

######################
#### Assumptions #####
#
# We want to draw a clear line between "infrastructure" and "domain".
# Our "domain" does not knowledge of a message broker.
# When we want to forward some data from the messager broker to the domain
# we use a simple entity called "Message".
#
# Regardless of the messaging system used, messages are the same and have 3 components:
# - a subject (always set)
# - some payload (possibly empty)
# - some headers (possibly empty)
#
# We do NOT make any more assumptions.

###########################################################
# We know that we need to receive messages on specific subjects.
# Let's start by describing the info contained in subjects.
###########################################################


@dataclass
class EventScope:
    """Metadata required to construct event subject.

    In this example application, events are delivered for a location and a device ID.
    """

    location: str
    device_id: int


###############################################################
# We also know that message are delivered with headers.
# So let's describe the info contained within message headers
###############################################################


@dataclass
class MeasurementMeta:
    """Metadata found in measurement event headers.

    In this example application, measurement events have one required metadata field and one optional.
    """

    test: bool
    unit: t.Optional[str]


#################################################################
# Define an event using the metadata created above
# We will see below why defining event is crucial in order to benefit from typechecking !
# The 4 generic typevars of an event are:
#   * the scope schema
#   * the payload schema
#   * the metadata schema
#   * the reply schema (in case event can be requested)
# Bring your cursor onto MEASUREMENT_EVENT to see type annotations
##################################################################

MEASUREMENT_EVENT = create_event(
    "measurement",
    "sensors.{location}.{device_id}.measure",
    schema=int,
    scope_schema=EventScope,
    metadata_schema=MeasurementMeta,
    description="An event holding device measurement as integer",
)


####################################################
# Define some other header metadata
####################################################


@dataclass
class ProcessingDoneMeta:
    """Metadata found in processing-done event headers"""

    process_duration: float


######################################################
# Define another event using above metadata
######################################################

PROCESSING_DONE = create_event(
    "processing-done",
    "sensors.{location}.{device_id}.processing_done",
    schema=t.Dict[str, int],
    scope_schema=EventScope,
    metadata_schema=ProcessingDoneMeta,
    description="An event indicating that a measurement has been processed",
)

######################################################################
# This is how we define a logical flow
# Right now, there is no processing logic, this is just about defining
# relations and scope
# Note that flow here is created as a global variable,
# but it can also be generated on the fly on application startup
# (contrary to events, which must be declared BEFORE in order to benefit the most from typechecking)
# A flow is also typed according to its source event
# Move your cursor on "flow" variable to see type annotations
######################################################################

MEASUREMENT_FLOW = create_flow(
    MEASUREMENT_EVENT,
    emits=[PROCESSING_DONE],
    scope={"location": "westus"},
)

########################################
# This is how we define a handler
########################################


@dataclass
class Handler:
    """An event handler.

    In order to unit test this handler, it's possible to provide a fake event bus during init.
    """

    bus: EventBus

    async def __call__(
        self, msg: Message[EventScope, int, MeasurementMeta, None]
    ) -> None:
        """Process messages for a specific event."""
        # Checkout the type annotations
        # That's all we know about a message, nothing more !
        # Note that message does not have concept of success of failure
        # If it is desired to implement result containers, do so in the type annotation
        # of the payload (and/or the headers)
        msg.subject
        msg.data
        msg.event
        msg.metadata
        msg.scope
        # Emit an event indicating that event was processed
        # Dependending on event bus provided at init, an error
        # may be raised because bus is not allowed to publish to event
        await self.bus.publish(
            # We do not target a suject, instead we target an event !
            PROCESSING_DONE,
            # mypy would tell us if data was not None (because event defines reply schema as None)
            data={"msg": 2},
            # mypy would tell us if scope was not ok right type
            scope=msg.scope,
            # same thing here, mypy would tell us if metadata were not of right type
            metadata=ProcessingDoneMeta(process_duration=0),
        )


###########################################
# Now let's define some instrumentation
# We will see right after how it is used
###########################################


class MyInstrumentation(PlayInstrumentation):
    def __init__(self) -> None:
        self.logger = logging.getLogger("demo")
        super().__init__()

    def play_starting(self, play: "Play") -> None:
        self.logger.info("Play starting")

    def play_started(self, play: "Play") -> None:
        self.logger.info("Play started")

    def play_failed(self, play: "Play", errors: t.List[BaseException]) -> None:
        self.logger.error(f"Play failed with errors: {errors}")

    def play_stopped(self, play: "Play") -> None:
        self.logger.warning("Play stopped")

    def play_stopping(self, play: "Play") -> None:
        self.logger.warning("Play stopping")

    def actor_starting(self, play: "Play", actor: Actor) -> None:
        if isinstance(actor, Subscriber):
            self.logger.info(
                f"Starting subscriber {actor.name}: event={actor.flow.source.name} subject={actor.flow.source._subject}"
            )
        else:
            self.logger.info(f"Starting producer: {actor.name}")

    def actor_started(self, play: "Play", actor: Actor) -> None:
        if isinstance(actor, Subscriber):
            self.logger.info(f"Subscriber started: {actor.name}")
        else:
            self.logger.info(f"Producer started: {actor.name}")

    def event_processed(
        self, play: "Play", actor: Actor, msg: Message[t.Any, t.Any, t.Any, t.Any]
    ) -> None:
        self.logger.info(
            f"Processed an event: actor={actor.name} event={msg.event.name}"
        )

    def event_received(
        self, play: "Play", actor: Actor, msg: Message[t.Any, t.Any, t.Any, t.Any]
    ) -> None:
        self.logger.info(
            f"Received an event: actor={actor.name} event={msg.event.name} location={msg.scope.location} device_id={msg.scope.device_id} unit={msg.metadata.unit}"
        )

    def event_processing_failed(
        self,
        play: "Play",
        actor: Actor,
        msg: Message[t.Any, t.Any, t.Any, t.Any],
        exc: BaseException,
    ) -> None:
        self.logger.error(
            f"Failed to process an event: actor={actor.name} event={msg.event.name} location={msg.scope.location} device_id={msg.scope.device_id} unit={msg.metadata.unit}",
            exc_info=exc,
        )


######################################################################
# The code below in the "plumbing" required to "start applications"
#
# At this point we need some publish/subscribe backend
# Once we have a pubsub backend we can create an event bus
######################################################################

bus = create_bus(NATSPubSub())

######################################################################
# And finally we can create a play
# It this line who tells:
#  The callable Handler will be used to process messages received by flow source event
#  Moreover, the handler can only publish/request events declared within flow
######################################################################

play = Play(
    bus=bus,
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
            "measurement-subscriber",
            # Subscribe will subscribe to flow source
            MEASUREMENT_FLOW,
            # Handler event bus is restricted according to the flow permissions
            Handler(bus.bind_flow(MEASUREMENT_FLOW)),
        ),
        # We could also create producers
        # Producer(flow=some_other_flow, task_factory=some_coroutine_function),
    ],
    # Use custom instrumentation
    instrumentation=MyInstrumentation(),
    # Auto-connect/disconnect the event bus
    auto_connect=True,
)
# Bonus: From the play alone, we can infer a DAG !
# Since each flow defines its source (if any) and the
# events it emits/requests, we can get a pretty good
# view of what's happening within the application !

# The benefits:
#  - The two most valuable benefits are:
#     * type checking everywhere
#     * the fact that we target events and not subjects
#  - Another benefit is the fact that we draw a clear limit
#    between domain and infrastructure.
#    Infrastructure deals with pubsub messages, payload, headers and subjects.
#    Domain deals with events messages, scope, data and metadata.
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
    logging.basicConfig(level="DEBUG", format="%(levelname)s - %(name)s - %(message)s")
    play.main()
