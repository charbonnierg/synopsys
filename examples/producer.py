"""An example illustrating how to publish events.

Usecases:
    => All the "gateways" which publish data into our systems
"""
import anyio
from dataclasses import dataclass
from synopsys import create_flow, create_bus, create_event, EventBus, Play, Producer
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

PRODUCER_FLOW = create_flow(emits=[DEVICE_EVENT])


async def produce(bus: EventBus) -> None:
    """Producer task."""
    while True:
        await bus.publish(DEVICE_EVENT, DeviceEvent("hello"))
        await anyio.sleep(1)


play = Play(
    create_bus(NATSPubSub()),
    actors=[Producer("device-event-producer", PRODUCER_FLOW, produce)],
)
