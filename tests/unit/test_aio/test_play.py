import asyncio
import typing as t

import pytest
import pytest_asyncio
from _pytest.fixtures import SubRequest
from anyio import fail_after

from synopsys import EventBus, Play, Producer, create_bus, create_event, create_flow
from synopsys.adapters import InMemoryPubSub, NATSPubSub


@pytest_asyncio.fixture
async def bus(request: SubRequest) -> t.AsyncIterator[EventBus]:
    """A fixture which returns an event bus."""
    cls = getattr(request, "param", InMemoryPubSub)
    bus = create_bus(cls())
    try:
        yield bus
    finally:
        await bus.disconnect()


class TestPlayProperties:
    def test_play_task_group_not_started(self):
        with pytest.raises(
            RuntimeError,
            match="Task group is not created yet.",
        ):
            Play(create_bus(InMemoryPubSub()), []).task_group


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "bus",
    [
        InMemoryPubSub,
        NATSPubSub,
    ],
    indirect=True,
    ids=["memory", "nats"],
)
class TestPlayLifecycle:
    async def test_play_start_stop_auto_connect(self, bus: EventBus):
        play = Play(bus=bus, actors=[], auto_connect=True)
        await play.start()
        # Check that we can publish something
        await play.bus.pubsub.publish("test", b"", {}, timeout=0.5)
        # Stop play
        await play.stop()

    async def test_play_stop_already_stopped(self, bus: EventBus):
        play = Play(bus=bus, actors=[])
        await play.stop()
        await play.stop()

    async def test_play_start_already_started(self, bus: EventBus):
        play = Play(bus=bus, actors=[])
        await play.start()
        await play.start()
        await play.stop()

    async def test_play_cancel_already_stopped(self, bus: EventBus):
        play = Play(bus=bus, actors=[])
        play.cancel()
        assert play.user_cancelled
        with pytest.raises(RuntimeError, match="Play has been cancelled"):
            await play.start()

    async def test_play_start_stop(self, bus: EventBus):
        play = Play(bus=bus, actors=[])
        await play.start()
        await play.stop()

    async def test_play_start_stop_using_asyncio_task(self, bus: EventBus):
        play = Play(bus=bus, actors=[])
        # Create a task
        task = asyncio.create_task(play())
        # Cancel task after some time
        await asyncio.sleep(0.1)
        assert not task.done()
        task.cancel()
        # Play should be stopped when task is cancelled
        with fail_after(0.2):
            await play.run_forever()
        # User cancelled must NOT be set because user did not call
        # cancel() method manually
        assert not play.user_cancelled

    async def test_play_start_and_wait_using_context_manager(self, bus: EventBus):
        # Expect a tiemout
        # If we don't get a timeout, it means that
        # context cancelled play on exit
        with pytest.raises(TimeoutError):
            # Context must be opened 200ms
            # Since we're using the memory bus, it's much more
            # than enough to confirm that play is not cancelled
            # on context exit
            with fail_after(0.2):
                async with Play(bus=bus, actors=[]):
                    # We expect to stay within the context for 200ms
                    pass
                # If we exit too early an error will be raised due to assert False
                assert (
                    False
                ), "Test should not reach this line. Exited from context too early."

    async def test_play_cancelled_error_is_not_propagated_to_main_context(
        self, bus: EventBus
    ):
        # Use a timeout to avoid waiting forever in case test fail
        # Unlike test start_and_wait test case, if TimeoutError is raised
        # it means that test failed
        with fail_after(0.2):
            async with Play(bus=bus, actors=[]) as play:
                # We expect to stay within the context for 200ms
                play.cancel()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "bus",
    [
        InMemoryPubSub,
        NATSPubSub,
    ],
    indirect=True,
    ids=["memory", "nats"],
)
class TestPlayProducers:
    async def test_play_start_with_a_single_producer(self, bus: EventBus):
        EVENT = create_event("test-event", "test.event")

        async def task(bus: EventBus) -> None:
            for _ in range(10):
                await bus.publish(EVENT, None, timeout=0.1)

        producer = Producer(
            flow=create_flow("test-producer", emits=[EVENT]),
            task_factory=task,
        )
        play = Play(bus, []).with_actors(producer)
        received: t.List[t.Any] = []
        with fail_after(1):
            # Start bus
            async with bus:
                # Start subscription
                async with bus.subscribe(EVENT) as sub:
                    # Start play
                    async with play:
                        # Iterate over messages received
                        async for msg in sub:
                            # Stop when 10 messares are received
                            received.append(msg)
                            if len(received) == 10:
                                break
                        # Cancel play
                        play.cancel()
