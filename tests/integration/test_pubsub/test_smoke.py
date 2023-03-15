import typing as t

import pytest
import pytest_asyncio
from _pytest.fixtures import SubRequest

from synopsys import EventBus, Message, create_event
from synopsys.adapters import InMemoryPubSub, NATSPubSub, PseudoJSONCodec
from synopsys.errors import BusDisconnectedError, SubscriptionClosedError


@pytest_asyncio.fixture
async def bus(request: SubRequest) -> t.AsyncIterator[EventBus]:
    """A fixture which returns an event bus."""
    cls = getattr(request, "param", InMemoryPubSub)
    bus = EventBus(cls(), codec=PseudoJSONCodec())
    async with bus.pubsub:
        yield bus


@pytest.mark.parametrize(
    "bus",
    [
        InMemoryPubSub,
        NATSPubSub,
    ],
    indirect=True,
    ids=["memory", "nats"],
)
class TestEventBusInterface:
    """Test the event bus interface."""

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
    async def test_event_bus_request_event(self, bus: EventBus):
        # Create some event
        event = create_event(
            "test-event",
            "test",
            schema=int,
            metadata_schema=t.Dict[str, str],
            reply_schema=int,
        )
        # Create a waiter which will listen for next event
        waiter = await bus.wait_in_background(event)
        # Create a pending request
        pending_request = await bus.request_in_background(
            event, data=12, metadata={"test": "somemeta"}, timeout=0.1
        )
        # Wait for request
        request = await waiter.wait()
        # Send a reply to the request
        await bus.reply(request, data=request.data + 1)
        # Await the pending request and confirm received data
        assert await pending_request.wait() == 13

    @pytest.mark.asyncio
    async def test_subscription_iterator_is_closed_on_context_exit(self, bus: EventBus):
        # Create some event
        event = create_event(
            "test-event", "test", schema=int, metadata_schema=t.Dict[str, str]
        )
        # Start a subscription
        async with bus.subscribe(event) as subscription:
            # Do nothing so that susbcription is started and closed
            pass
        # Check that event is not delivered when subscription is closed
        with pytest.raises(SubscriptionClosedError):
            async for _ in subscription:
                raise ValueError("No message was expected")

    @pytest.mark.asyncio
    async def test_subscription_closed_is_raised_on_context_exit(self, bus: EventBus):
        # Create some event
        event = create_event(
            "test-event", "test", schema=int, metadata_schema=t.Dict[str, str]
        )
        # Start a subscription
        async with bus.subscribe(event) as subscription:
            # Publish an event
            await bus.publish(
                event, data=12, metadata={"test": "somemeta"}, timeout=0.1
            )
        # Check that event is not delivered when subscription is closed
        with pytest.raises(SubscriptionClosedError):
            async for _ in subscription:
                raise ValueError("No message was expected")

    @pytest.mark.asyncio
    async def test_bus_disconnected_is_raised_on_publish_after_disconnection(
        self, bus: EventBus
    ):
        # Create some event
        event = create_event(
            "test-event", "test", schema=int, metadata_schema=t.Dict[str, str]
        )
        # Disconnect bus early
        await bus.disconnect()
        # Publish an event
        with pytest.raises(BusDisconnectedError):
            await bus.publish(
                event, data=12, metadata={"test": "somemeta"}, timeout=0.1
            )
