from typing import Callable, Dict, List, Coroutine
from logging import getLogger
from collections import defaultdict

from trio import Nursery


log = getLogger("anilibria.dispatch")
__all__ = ["Dispatch"]


class Dispatch:
    def __init__(self) -> None:
        self._registered_events: Dict[str, List[Callable[..., Coroutine]]] = defaultdict(list)
        self.nursery: Nursery = None  # noqa

    @staticmethod
    async def _call(coro: Callable[..., Coroutine], *args):
        try:
            await coro(*args)
        except Exception:  # noqa
            log.exception("")

    async def call(self, name: str, *args):
        log.debug(f"Dispatching event {name}")

        for coro in self._registered_events.get(name, []):
            self.nursery.start_soon(self._call, coro, *args)

    def register(self, name: str, coro: Callable[..., Coroutine]):
        self._registered_events[name].append(coro)

        log.debug(f"Added coro to {name} event. Total coros for this event: {self._registered_events[name]}")
