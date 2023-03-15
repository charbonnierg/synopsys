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


@dataclass
class EventScope:
    """Metadata required to construct event subject.

    In this example application, events are delivered for a location and a device ID.
    """

    location: str
    device_id: int


@dataclass
class MeasurementMeta:
    """Metadata found in measurement event headers.

    In this example application, measurement events have one required metadata field and one optional.
    """

    test: bool
    unit: t.Optional[str]


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


PROCESSING_DONE = create_event(
    "processing-done",
    "sensors.{location}.{device_id}.processing_done",
    schema=t.Dict[str, int],
    scope_schema=EventScope,
    metadata_schema=ProcessingDoneMeta,
    description="An event indicating that a measurement has been processed",
)

MEASUREMENT_FLOW = create_flow(
    MEASUREMENT_EVENT,
    emits=[PROCESSING_DONE],
    scope={"location": "westus"},
)


@dataclass
class Handler:
    bus: EventBus

    async def __call__(
        self, msg: Message[EventScope, int, MeasurementMeta, None]
    ) -> None:
        """Process messages for a specific event."""
        # Emit an event indicating that event was processed
        await self.bus.publish(
            PROCESSING_DONE,
            data={"msg": 2},
            scope=msg.scope,
            metadata=ProcessingDoneMeta(process_duration=0),
        )


bus = create_bus(NATSPubSub())

play = Play(
    bus=bus,
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
    # Auto-connect/disconnect the event bus
    auto_connect=True,
)

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG", format="%(levelname)s - %(name)s - %(message)s")
    play.main()
