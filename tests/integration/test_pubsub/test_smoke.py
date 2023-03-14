import typing as t

import pytest
import pytest_asyncio
from _pytest.fixtures import SubRequest

from synopsys import EventBus, Message, create_event
from synopsys.adapters import InMemoryPubSub, PseudoJSONCodec
from synopsys.interfaces import PubSubBackend

ADAPTERS: t.Dict[str, t.Type[PubSubBackend]] = {
    "memory": InMemoryPubSub,
}


@pytest_asyncio.fixture
async def bus(request: SubRequest) -> t.AsyncIterator[EventBus]:
    """A fixture which returns an event bus."""
    yield EventBus(InMemoryPubSub(), codec=PseudoJSONCodec())


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "bus",
    [
        "memory",
    ],
    indirect=True,
)
class TestEventBusInterface:
    """Test the event bus interface."""

    async def test_event_bus_publish(self, bus: EventBus):
        # Create some event
        event = create_event(
            "test-event", "test", schema=int, metadata_schema=t.Dict[str, str]
        )
        # Start waiting for event
        waiter = await bus.wait_in_background(event)
        # Publish an event
        await bus.publish(event, data=12, metadata={"test": "somemeta"}, timeout=0.1)
        # Confirm that event was received
        received_event = await waiter.wait()
        # Confirm event message
        assert received_event == Message(
            subject="test",
            scope=None,
            data=12,
            metadata={"test": "somemeta"},
            event=event,
        )

    async def test_event_bus_observe_event(self, bus: EventBus):
        # Create two different events
        target_event = create_event(
            "test-1", "test.1", schema=int, metadata_schema=t.Dict[str, str]
        )
        ignored_event = create_event(
            "test-2", "test.2", schema=int, metadata_schema=t.Dict[str, str]
        )
        # Create a waiter for a single event
        waiter = await bus.wait_in_background(target_event)
        # This event should be ignored by the waiter
        await bus.publish(
            ignored_event, data=0, metadata={"test": "somemeta"}, timeout=0.1
        )
        assert not waiter.task.done()
        # This event should be received by the waiter
        await bus.publish(
            target_event, data=12, metadata={"test": "somemeta"}, timeout=0.1
        )
        # Confirm that waiter received the message
        received_event = await waiter.wait(timeout=0.1)
        assert received_event == Message(
            subject="test.1",
            scope=None,
            data=12,
            metadata={"test": "somemeta"},
            event=target_event,
        )
