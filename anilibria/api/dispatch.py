from asyncio import get_event_loop
from typing import Callable, Dict, List, Coroutine
from logging import getLogger
from collections import defaultdict

from trio import open_nursery


log = getLogger("anilibria.dispatch")
__all__ = ["Dispatch"]


class Dispatch:
    def __init__(self) -> None:
        self.loop = get_event_loop()
        self._registered_events: Dict[str, List[Callable[..., Coroutine]]] = defaultdict(list)

    async def call(self, name: str, *args):
        log.debug(f"Dispatching event {name}")

        async with open_nursery() as nursery:
            for coro in self._registered_events.get(name, []):
                nursery.start_soon(coro, *args)

    def register(self, name: str, coro: Callable[..., Coroutine]):
        self._registered_events[name].append(coro)

        log.debug(f"Added coro to {name} event. Total coros for this event: {self._registered_events[name]}")
