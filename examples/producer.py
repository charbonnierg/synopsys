"""An example illustrating how to publish events.

Usecases:
    => All the "gateways" which publish data into our systems
"""
from dataclasses import dataclass

import anyio

from synopsys import EventBus, Play, Producer, create_bus, create_event, create_flow
from synopsys.adapters import NATSPubSub


@dataclass
class DeviceEvent:
    msg: str


@dataclass
class DeviceScope:
    device_id: str
    event_type: str


DEVICE_EVENT = create_event(
    "device-event",
    "device.{device_id}.{event_type}",
    schema=DeviceEvent,
    scope_schema=DeviceScope,
)

PRODUCER_FLOW = create_flow("device-event-producer", emits=[DEVICE_EVENT])


async def produce(bus: EventBus) -> None:
    """Producer task."""
    while True:
        await bus.publish(DEVICE_EVENT, DeviceEvent("hello"))
        await anyio.sleep(1)


play = Play(
    create_bus(NATSPubSub()),
    actors=[Producer(PRODUCER_FLOW, produce)],
)
# Hypothetical:
# Assuming we have a list of flows
# We can check if provided actors are enough
# to "run" all flows
# It may not be simple

# How do we map a list of flows and a play ?
# Maybe we would register actors one by one ?

# Hypothetical API
# play = Play(flows=flows)
# for actor in [
#   Producer(SOME_FLOW)
# ]
