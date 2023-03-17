import sys
import typing as t
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from types import TracebackType

from anyio import Event, create_task_group, get_cancelled_exc_class, run
from anyio.abc._tasks import TaskGroup

from ..entities.actors import Actor, Producer, Service, Subscriber
from ..interfaces.instrumentation import PlayInstrumentation
from .bus import EventBus


@dataclass
class Play:
    bus: EventBus
    actors: t.List[Actor] = field(default_factory=list)
    instrumentation: PlayInstrumentation = field(
        default_factory=PlayInstrumentation, repr=False
    )
    auto_connect: bool = False

    def __post_init__(self) -> None:
        self._task_group: t.Optional[TaskGroup] = None
        self._exit_stack: t.Optional[AsyncExitStack] = None
        self.stopped: t.Optional[Event] = None
        self.user_cancelled: bool = False

    @property
    def task_group(self) -> TaskGroup:
        if self._task_group is None:
            raise RuntimeError(
                "Task group is not created yet. Use the .start() method or enter async context in order to start play."
            )
        return self._task_group

    def with_actors(self, *actors: Actor) -> "Play":
        """Add actors to the play."""
        self.actors.extend(actors)
        return self

    async def _on_exit(self) -> None:
        if self.stopped:
            self.stopped.set()

    async def _create_susbcriber_loop(
        self, actor: Subscriber[t.Any, t.Any, t.Any, t.Any, t.Any]
    ) -> None:
        event = actor.flow.event
        callback = actor.handler
        async with self.bus.subscribe(event, queue=actor.queue) as subscription:
            self.instrumentation.actor_started(self, actor)
            async for msg in subscription:
                self.instrumentation.event_received(self, actor, msg)
                try:
                    await callback(msg)
                    self.instrumentation.event_processed(self, actor, msg)
                except Exception as exc:
                    self.instrumentation.event_processing_failed(self, actor, msg, exc)
                    continue

    async def _create_service_loop(
        self,
        actor: Service[t.Any, t.Any, t.Any, t.Any, t.Any],
    ) -> None:
        event = actor.flow.command
        callback = actor.handler
        async with self.bus.subscribe(event, queue=actor.queue) as subscription:
            self.instrumentation.actor_started(self, actor)
            async for msg in subscription:
                self.instrumentation.event_received(self, actor, msg)
                try:
                    reply = await callback(msg)
                    await self.bus.reply(msg, data=reply.data, metadata=reply.metadata)
                    self.instrumentation.event_processed(self, actor, msg)
                except Exception as exc:
                    self.instrumentation.event_processing_failed(self, actor, msg, exc)
                    continue

    async def _start_actors(self) -> None:
        for actor in self.actors:
            self.instrumentation.actor_starting(self, actor)
            if isinstance(actor, Producer):
                # Start producer
                self.task_group.start_soon(
                    actor.task_factory,
                    self.bus.bind_flow(actor.flow),
                    name=actor.flow.name,
                )
                # Continue in order to start next actor
                continue
            if isinstance(actor, Subscriber):
                # Start subscriber
                self.task_group.start_soon(
                    self._create_susbcriber_loop, actor, name=actor.flow.name
                )
                # Continue in order to start next actor
                continue
            if isinstance(actor, Service):
                # Start service
                self.task_group.start_soon(
                    self._create_service_loop, actor, name=actor.flow.name
                )
                # Continue in order to start next actor
                continue
            raise TypeError(
                f"Invalid actor type: {type(actor)}. Use either `synopsys.Producer or synopsys.Subscriber class."
            )

    async def start(self) -> None:
        """Start play"""
        if self.user_cancelled:
            raise RuntimeError("Play has been cancelled")
        if self._task_group is not None:
            return
        self.instrumentation.play_starting(self)
        # Create and start exist task
        self._exit_stack = AsyncExitStack()
        await self._exit_stack.__aenter__()
        # Auto-connect when needed
        if self.auto_connect:
            await self._exit_stack.enter_async_context(self.bus)
        # Create and start task group
        self._task_group = await self._exit_stack.enter_async_context(
            create_task_group()
        )
        # Try to create actors
        try:
            await self._start_actors()
        except BaseException as _exc:
            exc_type, exc, tb = sys.exc_info()
            self.instrumentation.play_failed(self, [_exc])
            self._task_group.cancel_scope.cancel()
            await self._exit_stack.__aexit__(exc_type, exc, tb)
            raise
        # Push async callback
        self._exit_stack.push_async_callback(self._on_exit)
        self.instrumentation.play_started(self)

    def cancel(self) -> None:
        self.user_cancelled = True
        if self._task_group and not self._task_group.cancel_scope.cancel_called:
            self._task_group.cancel_scope.cancel()

    async def stop(self) -> None:
        """Stop play"""
        if self._exit_stack is None:
            return
        self.instrumentation.play_stopping(self)
        try:
            self.task_group.cancel_scope.cancel()
            await self._exit_stack.__aexit__(*sys.exc_info())
        finally:
            self.instrumentation.play_stopped(self)

    async def run_forever(self) -> None:
        if self.stopped is None:
            self.stopped = Event()
        # Do we want to raise a CancelledError
        # when we cancel from outside ?
        try:
            await self.stopped.wait()
        except BaseException:
            await self.stop()
            raise

    async def __call__(self) -> None:
        await self.start()
        await self.run_forever()

    async def __aenter__(self) -> "Play":
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: t.Optional[t.Type[BaseException]] = None,
        exc: t.Optional[BaseException] = None,
        traceback: t.Optional[TracebackType] = None,
    ) -> None:
        try:
            await self.run_forever()
        except get_cancelled_exc_class():
            if self.user_cancelled:
                return
            raise

    def main(self) -> None:
        try:
            return run(self)
        except KeyboardInterrupt:
            pass
